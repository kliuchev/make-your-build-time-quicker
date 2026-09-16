import Feature32Domain

public enum Feature32DataRepository {
    public static func load(_ id: Int) -> Feature32DomainModel {
        Feature32DomainModel(id: id, title: "Feature 32")
    }
}
