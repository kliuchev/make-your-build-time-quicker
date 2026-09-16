// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature13Data",
    products: [.library(name: "Feature13Data", targets: ["Feature13Data"])],
    dependencies: [.package(path: "../Feature13Domain")],
    targets: [.target(name: "Feature13Data", dependencies: [.product(name: "Feature13Domain", package: "Feature13Domain")])]
)
