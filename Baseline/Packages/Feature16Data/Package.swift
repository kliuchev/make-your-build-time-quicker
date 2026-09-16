// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature16Data",
    products: [.library(name: "Feature16Data", targets: ["Feature16Data"])],
    dependencies: [.package(path: "../Feature16Domain")],
    targets: [.target(name: "Feature16Data", dependencies: [.product(name: "Feature16Domain", package: "Feature16Domain")])]
)
