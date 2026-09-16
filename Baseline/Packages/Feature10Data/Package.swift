// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature10Data",
    products: [.library(name: "Feature10Data", targets: ["Feature10Data"])],
    dependencies: [.package(path: "../Feature10Domain")],
    targets: [.target(name: "Feature10Data", dependencies: [.product(name: "Feature10Domain", package: "Feature10Domain")])]
)
