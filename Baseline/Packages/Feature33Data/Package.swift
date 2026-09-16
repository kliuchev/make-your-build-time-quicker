// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature33Data",
    products: [.library(name: "Feature33Data", targets: ["Feature33Data"])],
    dependencies: [.package(path: "../Feature33Domain")],
    targets: [.target(name: "Feature33Data", dependencies: [.product(name: "Feature33Domain", package: "Feature33Domain")])]
)
